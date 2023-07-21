<script>
    import { inview } from 'svelte-inview';
    import { fade } from 'svelte/transition';

    let isInView;
</script>

<header
    use:inview={{ unobserveOnEnter: true, rootMargin: '-20%' }}
    on:change={({ detail }) => isInView = detail.inView}
    class="absolute top-0 left-0 w-full text-white"
>
    {#if isInView}
        <div class="container mx-auto px-6 py-8" in:fade>
            <a href="/" in:fade={{ duration: 300 }}>
                <h1 class="text-3xl uppercase">
                    <span class="font-light">Team</span>
                    <span class="font-semibold">Sigmoid</span>
                </h1>
            </a>
        </div>
    {/if}
</header>