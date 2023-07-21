<script>
    import { Label } from "flowbite-svelte";
    import Dropzone from "svelte-file-dropzone/Dropzone.svelte";
    import { XIcon } from "svelte-feather-icons";
    import { slide } from 'svelte/transition';

    export let visible = false;
    export let features = [];
    let preview_images = [];

    const handleFilesSelect = (e) => {
        const { acceptedFiles } = e.detail;
        features = [...features, ...acceptedFiles];
        preview_images = [...preview_images, ...acceptedFiles.map(file => URL.createObjectURL(file))];
    }

    const removeImage = (index) => {
        features = features.filter((_, i) => i !== index);
        preview_images = preview_images.filter((_, i) => i !== index);
    }
</script>

<button
    on:click={() => visible = false}
    class={[
        'fixed top-0 left-0 w-full h-full bg-black/60 backdrop-blur z-10 transition cursor-auto',
        visible ? '' : 'opacity-0 pointer-events-none'
    ].join(' ')}
></button>

<aside
    class={[
        'bg-white p-4 w-[400px] border-l border-primary overflow-y-auto fixed top-0 right-0 z-20 h-screen',
        'overflow-auto transition',
        visible ? 'translate-x-0' : 'translate-x-full'
    ].join(' ')}
>
    <div class="flex justify-end mb-2">
        <button type="button" on:click={() => visible = false}>
            <XIcon />
        </button>
    </div>

    <Label for="features" class="uppercase text-sm opacity-60 font-bold">Upload Figma designs:</Label>
    <div class="mt-2 text-center">
        <Dropzone
            on:drop={handleFilesSelect}
            accept="image/*"
            containerClasses="!rounded-lg"
        />
    </div>

    {#if preview_images.length}
        {#key preview_images}
            <div class="grid grid-cols-2 gap-2 mt-4" in:slide>
                {#each preview_images as image, index}
                    <div class="relative rounded-lg overflow-hidden">
                        <img alt="Preview" src={image} class="w-full object-contain" />
                        <div class="absolute top-0 left-0 w-full h-full bg-gradient-to-bl from-black/60">
                            <button class="cursor-pointer flex ml-auto mt-2 pr-2" on:click={() => removeImage(index)}>
                                <XIcon class="text-white" size="18" />
                            </button>
                        </div>
                    </div>
                {/each}
            </div>
        {/key}
    {/if}
</aside>