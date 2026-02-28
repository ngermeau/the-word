<script lang="ts">
	import { onMount } from 'svelte';
	import { findAvailablePosition, drawWord } from '$lib/utils.js';
	import type { PageData } from './$types';

	export let data: PageData;

	onMount(() => {
		// Use the frequencies data from the server load function
		const frequencies = data.data?.data || [];

		// Convert to array if it's an object (depending on your API response format)
		let wordsArray = Array.isArray(frequencies)
			? frequencies
			: Object.entries(frequencies).map(([word, count]) => ({ word, count }));

		const RATIO = 1.414; // augmented fourth
		const BASE = 1.414; // rem
		const STEPS = 8;
		const typeScale = Array.from({ length: STEPS }, (_, i) =>
			parseFloat((BASE * Math.pow(RATIO, i)).toFixed(3))
		);
		// typeScale ≈ [1, 1.414, 2, 2.828, 4, 5.657, 8, 11.314]

		const maxCount = Math.max(...wordsArray.map((w) => w[1]));
		const minCount = Math.min(...wordsArray.map((w) => w[1]));
		const range = maxCount - minCount || 1;
		wordsArray = wordsArray.map((w) => {
			const normalized = (w[1] - minCount) / range;
			const stepIndex = Math.min(Math.floor(normalized * STEPS), STEPS - 1);
			return [w[0], typeScale[stepIndex]];
		});

		wordsArray.sort(() => Math.random() - 0.5);
		wordsArray.forEach((word) => {
			let wordPosition = findAvailablePosition(word);
			if (wordPosition) drawWord(word, wordPosition);
		});
	});
</script>

<div class="container"></div>

<style>
	.container {
		height: 100%;
		display: grid;
		grid-template-columns: repeat(50, 1fr);
		grid-template-rows: repeat(50, 1fr);
		place-items: start start;
	}
</style>
