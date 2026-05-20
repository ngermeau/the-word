import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { supabaseAdmin } from '$lib/supabaseAdmin';
import nlp from 'compromise';

const COUNTER_SIZE = 100;

function count(words: string[]): [string, number][] {
	const freq: Record<string, number> = {};
	for (const w of words) {
		const key = w.toLowerCase();
		freq[key] = (freq[key] ?? 0) + 1;
	}
	return Object.entries(freq)
		.sort((a, b) => b[1] - a[1])
		.slice(0, COUNTER_SIZE);
}

export const GET: RequestHandler = async () => {
	const today = new Date().toISOString().split('T')[0];

	const { data, error } = await supabaseAdmin
		.from('daily_articles')
		.select('title')
		.eq('date', today);

	if (error) return json({ error: error.message }, { status: 500 });
	if (!data?.length) return json({ error: 'No articles found for today' }, { status: 404 });

	const text = data.map((r) => r.title).join(' ');
	const doc = nlp(text);

	const properNouns = doc.match('#ProperNoun').out('array') as string[];
	const commonNouns = doc.match('#Noun').not('#ProperNoun').out('array') as string[];

	const properNounsCount = count(properNouns);
	const commonNounsCount = count(commonNouns);

	const { error: upsertError } = await supabaseAdmin
		.from('daily_articles_analysis')
		.upsert({
			date: today,
			proper_nouns: properNouns,
			proper_nouns_count: properNounsCount,
			common_nouns: commonNouns,
			common_nouns_count: commonNounsCount
		});

	if (upsertError) return json({ error: upsertError.message }, { status: 500 });

	return json({
		date: today,
		articles: data.length,
		proper_nouns: properNounsCount.slice(0, 10),
		common_nouns: commonNounsCount.slice(0, 10)
	});
};
