<script>
    import { onMount } from "svelte";

    let windowWidth = 1920;

    export let loading = false;
    export let results = [];
    export let similarity = null;

    onMount(() => windowWidth = window.innerWidth);
</script>

{#if results.length}
    <div class="container mx-auto px-4 py-12 grid grid-cols-6 gap-6">
        {#each results as image, i}
            <div class="relative rounded-lg overflow-hidden shadow transition hover:shadow-lg">
                <img
                    src={image}
                    alt="Mobile"
                    width="375"
                    height="810"
                    draggable="false"
                />

                {#if similarity}
                    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
                        <div class="text-sm font-semibold opacity-80 whitespace-nowrap">Look and Feel:</div>
                        <div class="text-xl font-semibold">{(similarity[0][i] * 100).toFixed(2)}</div>

                        <div class="text-sm font-semibold opacity-80 whitespace-nowrap mt-2">Pixel comparison:</div>
                        <div class="text-xl font-semibold">{(similarity[1][i] * 100).toFixed(2)}</div>
                    </div>
                {/if}
            </div>
        {/each}
    </div>
{:else}
    <div class="text-center mt-6 text-sm">
        The results will appear here.
    </div>
{/if}

{#if loading}
    <div class="fixed bottom-0 left-0 z-100 loading" style="--width: {windowWidth}px">
        <img
            src="/loading.png"
            width="1193"
            height="773"
            alt="Loading"
            class="w-32"
        />
    </div>
{/if}

<style>
    @keyframes progress {
        0% { transform: translateX(0) scaleX(-1); }
        49% { transform: translateX(calc(var(--width) - 100%)) scaleX(-1); }
        50% { transform: translateX(calc(var(--width) - 100%)) scaleX(1); }
        100% { transform: translateX(0) scaleX(1); }
    }

    .loading img {
        animation: progress 4s infinite;
    }
</style>
