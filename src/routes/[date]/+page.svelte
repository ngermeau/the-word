<script lang="ts">
  import { onMount } from "svelte";
  import {
    findAvailablePosition,
    drawWord,
    numberOfRows,
    numberOfCols,
  } from "$lib/utils.js";
  import { gsap } from "gsap";
  import type { PageData } from "./$types";

  export let data: PageData;

  onMount(async () => {
    await document.fonts.load('1em "Bebas Neue"');

    let wordsArray = data.words ?? [];
    const RATIO = 1.414;
    const STEPS = 8;
    const baseScale = Array.from({ length: STEPS }, (_, i) =>
      parseFloat(Math.pow(RATIO, i).toFixed(3)),
    );

    // Assign step indices from frequency
    const maxCount = Math.max(...wordsArray.map((w) => w[1]));
    const minCount = Math.min(...wordsArray.map((w) => w[1]));
    const range = maxCount - minCount || 1;
    const wordSteps = wordsArray.map((w) => {
      const normalized = (w[1] - minCount) / range;
      return Math.min(Math.floor(normalized * STEPS), STEPS - 1);
    });

    // Measure words at BASE=1 to find adaptive scale
    const cellWidth = window.innerWidth / numberOfCols;
    const cellHeight = window.innerHeight / numberOfRows;
    let totalCells = 0;
    wordsArray.forEach((w, i) => {
      const elem = document.createElement("span");
      elem.style.cssText = `position:absolute;visibility:hidden;font-family:inherit;text-transform:uppercase;font-size:${baseScale[wordSteps[i]]}vw;padding:1px 2px`;
      elem.textContent = w[0];
      document.body.appendChild(elem);
      totalCells +=
        Math.ceil(elem.offsetWidth / cellWidth) *
        Math.ceil(elem.offsetHeight / cellHeight);
      document.body.removeChild(elem);
    });

    // Scale BASE so words fill 75% of the grid
    const BASE = Math.max(
      1,
      Math.sqrt((numberOfRows * numberOfCols * 0.75) / totalCells),
    );
    const typeScale = baseScale.map((s) => parseFloat((s * BASE).toFixed(3)));
    wordsArray = wordsArray.map((w, i) => [w[0], typeScale[wordSteps[i]]]);
    wordsArray.push([data.date, typeScale[2], "#ffffff"]);
    wordsArray.sort((a, b) => b[1] - a[1]);
    // Anchor the largest word at center; shuffle the rest so size doesn't dictate radial position.
    for (let i = wordsArray.length - 1; i > 1; i--) {
      const j = 1 + Math.floor(Math.random() * i);
      [wordsArray[i], wordsArray[j]] = [wordsArray[j], wordsArray[i]];
    }
    console.log(
      "placement order:",
      wordsArray.map((w) => w[0]).slice(0, 10),
    );

    const elements: HTMLElement[] = [];
    wordsArray.forEach((word) => {
      let wordPosition = findAvailablePosition(word);
      if (wordPosition) {
        const el = drawWord(word, wordPosition);
        if (el) elements.push(el);
      }
    });

    gsap.fromTo(
      elements,
      { opacity: 0 },
      {
        opacity: 1,
        duration: 1,
        ease: "power2.out",
        stagger: 0.01,
      },
    );
  });
</script>

<div class="container"></div>

<style>
  .container {
    width: 100vw;
    height: 100vh;
    display: grid;
    grid-template-columns: repeat(50, 1fr);
    grid-template-rows: repeat(50, 1fr);
    place-items: center;
  }
</style>
