<script lang="ts">
	import { onMount } from 'svelte';
	import { findAvailablePosition, drawWord } from '$lib/utils.js';
	import type { PageData } from './$types';

	export let data: PageData;

	onMount(() => {
		// Use the frequencies data from the server load function
		const frequencies = data.frequencies || [];

		// Convert to array if it's an object (depending on your API response format)
		let wordsArray = Array.isArray(frequencies) ? frequencies : Object.entries(frequencies).map(([word, count]) => ({ word, count }));

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
