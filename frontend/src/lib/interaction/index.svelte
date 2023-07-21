<script>
    import Search from '$lib/interaction/search.svelte';
    import Output from '$lib/interaction/output.svelte';

    let loading = false, results = [];

    const search = async ({ detail }) => {
        const url = import.meta.env.VITE_PUBLIC_BACKEND_URL;
        if (loading) return;
        loading = true;

        let formData = new FormData;
        formData.append('url', detail.url);
        for (let image of detail.features)
            formData.append('feature_images', image);
        let data = await fetch(`${url}/api/upload`, {
            method: 'POST',
            body: formData
        })
        const { hash, images } = await data.json();
        results = images.map(image => `/uploads/${hash}/inputs/${image}`);

        formData = new FormData;
        formData.append('hash', hash);
        formData.append('filters', JSON.stringify(detail.filters));
        if (detail.features.length) {
            data = await fetch(`${url}/api/train`, { method: 'POST', body: formData });
            await data.json();
        }

        data = await fetch(`${url}/api/generate_score`, {
            method: 'POST',
            body: formData
        })
        data = await data.json();
        console.log(data);

        loading = false;
    }
</script>

<Search on:search={search} />
<Output loading={loading} results={results} />

