<script>
	import '../app.scss';

    import Header from '$lib/header.svelte';
    import Sidebar from '$lib/sidebar.svelte';
</script>

<div class="flex flex-col min-h-screen">
    <Header />
    <section class="flex justify-between w-full flex-1">
        <main class="container mx-auto py-6 px-4"><slot /></main>
        <Sidebar />
    </section>
</div>