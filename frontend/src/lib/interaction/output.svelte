<script>
    import { onMount } from "svelte";

    let windowWidth = 1920;

    export let loading = false;
    export let results = [];

    onMount(() => windowWidth = window.innerWidth);
</script>

{#if results.length}
    <div class="container mx-auto px-4 py-6 grid grid-col-6 gap-4">
        {#each results as image}
            <img
                class="rounded-full shadow transition hover:shadow-lg"
                src={image}
                alt="Mobile"
                width="375"
                height="810"
                draggable="false"
            />
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
