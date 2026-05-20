import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { supabaseAdmin } from '$lib/supabaseAdmin';
import { pipeline, type TranslationPipeline } from '@huggingface/transformers';
import Parser from 'rss-parser';
import { createHash } from 'crypto';
import { readFileSync } from 'fs';
import { resolve } from 'path';
import yaml from 'js-yaml';

const MAX_ARTICLES_PER_SOURCE = 20;

const LANG_MAP: Record<string, string> = {
	fr: 'fra_Latn',
	es: 'spa_Latn',
	de: 'deu_Latn',
	nl: 'nld_Latn',
	it: 'ita_Latn',
	pt: 'por_Latn',
	ar: 'ara_Arab'
};

let translator: TranslationPipeline | null = null;
async function getTranslator(): Promise<TranslationPipeline> {
	if (!translator)
		translator = (await pipeline(
			'translation',
			'Xenova/nllb-200-distilled-600M'
		)) as TranslationPipeline;
	return translator;
}

async function translateToEn(text: string, language: string): Promise<string> {
	if (language === 'en' || !LANG_MAP[language]) return text; //not that great
	const t = await getTranslator();
	const result = await t(text, { src_lang: LANG_MAP[language], tgt_lang: 'eng_Latn' });
	const output = Array.isArray(result) ? result : [result];
	return (output[0] as { translation_text: string }).translation_text;
}

type Newspaper = { name: string; rss_url: string; language: string };

export const GET: RequestHandler = async () => {
	const today = new Date().toISOString().split('T')[0];
	const newspapers = yaml.load(
		readFileSync(resolve('static/newspapers.yaml'), 'utf8')
	) as Newspaper[];

	const rssParser = new Parser();
	let totalInserted = 0;

	for (const newspaper of newspapers) {
		try {
			const feed = await rssParser.parseURL(newspaper.rss_url);
			const articles = [];

			for (const entry of feed.items.slice(0, MAX_ARTICLES_PER_SOURCE)) {
				if (!entry.title) continue;
				const title = await translateToEn(entry.title, newspaper.language);
				const id = createHash('md5').update(`${title}${newspaper.name}${today}`).digest('hex');
				articles.push({ id, title, source: newspaper.name, date: today });
			}

			if (articles.length) {
				const { error } = await supabaseAdmin
					.from('daily_articles')
					.upsert(articles, { onConflict: 'id', ignoreDuplicates: true });
				if (error) console.error(`Supabase error for ${newspaper.name}:`, error);
				else totalInserted += articles.length;
			}
		} catch (err) {
			console.error(`Failed to fetch ${newspaper.name}:`, err);
		}
	}

	return json({ inserted: totalInserted, date: today });
};
