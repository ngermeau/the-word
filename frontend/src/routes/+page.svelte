<script>
	import { onMount } from 'svelte';
	import data from '$lib/newdata.json';
	import { findAvailablePosition, drawWord } from '$lib/utils.js';

	onMount(() => {
		data.sort(() => Math.random() - 0.5);
		data.forEach((word) => {
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
