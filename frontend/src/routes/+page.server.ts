import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => {
	// Get today's date in YYYY-MM-DD format
	const today = new Date().toISOString().split('T')[0];

	// Fetch frequencies from your FastAPI backend
	// Update this URL to match your API server address
	const apiUrl = `http://localhost:8000/frequencies/${today}`;

	try {
		const response = await fetch(apiUrl);

		if (!response.ok) {
			console.error('Failed to fetch frequencies:', response.status);
			return {
				frequencies: []
			};
		}

		const frequencies = await response.json();

		// Handle "Not available" response from API
		if (frequencies === "Not available") {
			return {
				frequencies: []
			};
		}

		return {
			frequencies
		};
	} catch (error) {
		console.error('Error fetching frequencies:', error);
		return {
			frequencies: []
		};
	}
};
