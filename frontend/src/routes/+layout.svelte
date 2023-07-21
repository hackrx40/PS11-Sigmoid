<script>
	import '../app.scss';

    import Header from '$lib/header.svelte';
</script>

<div class="flex flex-col min-h-screen">
    <Header />
    <main class="w-full"><slot /></main>
</div>