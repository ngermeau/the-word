import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch, params }) => {
	const date = params.date;
	const apiUrl = `http://localhost:8000/theword/${date}`;
	console.log(apiUrl);
	try {
		const response = await fetch(apiUrl);
		if (!response.ok) {
			console.error(`API request failed with status ${response.status}`);
			return {
				data: [],
				error: `Failed to fetch data: ${response.statusText}`
			};
		}

		const data = await response.json();

		return {
			data
		};
	} catch (error) {
		console.error('Error fetching words:', error);
		return {
			data: [],
			error: error instanceof Error ? error.message : 'An unknown error occurred'
		};
	}
};
