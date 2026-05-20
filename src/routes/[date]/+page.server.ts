import type { PageServerLoad } from './$types';
import { supabaseAdmin } from '$lib/supabaseAdmin';

export const load: PageServerLoad = async ({ params }) => {
	const { date } = params;

	const { data, error } = await supabaseAdmin
		.from('daily_articles_analysis')
		.select('proper_nouns_count, common_nouns_count')
		.eq('date', date)
		.single();

	if (error || !data) {
		return { words: [], date };
	}

	const words = [
		...((data.proper_nouns_count as [string, number][]) ?? []),
		...((data.common_nouns_count as [string, number][]) ?? [])
	];

	return { words, date };
};
