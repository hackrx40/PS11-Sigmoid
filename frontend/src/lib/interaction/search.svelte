<script>
    import { SearchIcon } from 'svelte-feather-icons';
</script>

<form class="flex mx-auto text-center py-8 flex-col max-w-[600px]">
    <div class="relative">
        <input
            id="search"
            class="w-full rounded-full pl-6 pr-12 py-2 text-lg border-2 border-primary outline-none"
            placeholder="Enter URL here..."
        />
        <button class="absolute top-1/2 right-4 -translate-y-1/2 cursor-pointer" type="submit">
            <SearchIcon />
        </button>
    </div>
</form>