<script>
    import { inview } from 'svelte-inview';
    import { fly } from 'svelte/transition';

    let isInView;
</script>

<header
    use:inview={{ unobserveOnEnter: true }}
    on:change={({ detail }) => isInView = detail.inView}
    class="absolute top-0 left-0 w-full text-white z-10"
>
    {#if isInView}
        <div class="container mx-auto px-6 py-8" in:fly={{ x: -40 }}>
            <a href="/">
                <h1 class="text-3xl uppercase flex gap-2">
                    <span class="font-light">Team</span>
                    <span class="font-semibold">Sigmoid</span>
                </h1>
            </a>
        </div>
    {/if}
</header>