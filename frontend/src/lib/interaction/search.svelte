<script>
    import { SearchIcon } from 'svelte-feather-icons';
</script>

<form class="flex mx-auto text-center py-8 flex-col max-w-[600px]">
    <img
        alt="Working"
        class="w-32 mx-auto"
        draggable="false"
        height="150"
        src="/work.svg"
        width="150"
    />

    <div class="mt-4 mb-6">
        <h1 class="font-bold text-4xl">Enter the site URL</h1>
        <p class="max-w-[600px] mx-auto text-sm opacity-80 mt-2">
            We will compare the results from the URL against different screen resolution to provide you a valuable
            output with the information saying how much similarity does it follow with Bajaj website.
        </p>
    </div>

    <div class="relative">
        <input
            class="w-full rounded-full pl-6 pr-12 py-2 text-lg border-2 border-primary outline-none transition focus:shadow-lg"
            id="search"
            placeholder="Enter URL here..."
        />
        <button class="absolute top-1/2 right-4 -translate-y-1/2 cursor-pointer" type="submit">
            <SearchIcon />
        </button>
    </div>
</form>