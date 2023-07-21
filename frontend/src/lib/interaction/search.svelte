<script>
    import { SearchIcon, UploadIcon } from 'svelte-feather-icons';
    import Sidebar from '$lib/interaction/sidebar.svelte';

    let sidebarVisible = false;

    const filterLabels = ['button', 'text', 'image', 'link'];
    const filters = {
        button: false,
        text: false,
        image: false,
        link: false,
    }

    const getLabel = label => `${label[0].toUpperCase()}${label.slice(1)}s`;
</script>

<form class="text-center py-8 pt-32 relative min-h-[500px] w-full text-white flex">
    <img
        src="/background.jpg"
        alt="Background"
        width="4288"
        height="2848"
        class="absolute top-0 left-0 w-full h-full object-cover z-[-1] brightness-[0.3]"
        draggable="false"
    />

    <div class="max-w-[600px] m-auto">
        <div class="mb-8">
            <h1 class="font-bold text-4xl">Enter the site URL to test</h1>
            <p class="mx-auto text-sm mt-4">
                We will compare the difference between the input and the reference images and output the comparison value.
            </p>
        </div>

        <div class="text-black flex gap-4 w-full">
            <div class="relative w-full">
                <input
                    class="w-full rounded-full pl-6 pr-12 py-2 text-lg outline-none transition focus:shadow-lg"
                    id="search"
                    placeholder="Enter URL here..."
                />
                <button class="absolute top-1/2 right-4 -translate-y-1/2 cursor-pointer" type="submit">
                    <SearchIcon size="24" />
                </button>
            </div>

            <button
                class="bg-white rounded-full outline-none w-[44px] h-[44px] grid place-content-center shrink-0"
                type="button"
                on:click={() => sidebarVisible = true}
            >
                <UploadIcon size="20" />
            </button>
        </div>

        <div class="mt-12">
            Ignore:

            {#each filterLabels as filter}
                <button
                    class={[
                        'ml-2 px-5 py-1.5 rounded-full border border-white text-sm font-bold transition',
                        'hover:scale-105',
                        filters[filter] ? 'bg-white text-black' : 'text-white',
                    ].join(' ')}
                    on:click={() => filters[filter] = !filters[filter]}
                    type="button"
                >
                    {getLabel(filter)}
                </button>
            {/each}
        </div>
    </div>
</form>

<Sidebar bind:visible={sidebarVisible} />