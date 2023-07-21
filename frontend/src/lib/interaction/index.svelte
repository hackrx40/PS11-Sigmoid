<script>
    import Search from '$lib/interaction/search.svelte';
    import Output from '$lib/interaction/output.svelte';
    import { onMount } from "svelte";

    let loading = false, windowWidth = 1920;

    onMount(() => windowWidth = window.innerWidth);
</script>

<Search on:search={() => loading = true} />
<Output />

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
