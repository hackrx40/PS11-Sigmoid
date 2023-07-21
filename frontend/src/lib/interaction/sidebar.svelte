<script>
    import { Label, Toggle } from "flowbite-svelte";
    import Dropzone from "svelte-file-dropzone/Dropzone.svelte";
    import { XIcon } from "svelte-feather-icons";

    export let visible = false;

    let feature_images = [], preview_images = [];
    let reference = false, filters = {
        button: true,
        text: true,
        image: true,
        link: true
    };

    const handleFilesSelect = (e) => {
        const { acceptedFiles } = e.detail;
        feature_images = [...feature_images, ...acceptedFiles];
        preview_images = [...preview_images, ...acceptedFiles.map(file => URL.createObjectURL(file))];
        reference = !!feature_images.length;
    }

    const removeImage = (index) => {
        feature_images = feature_images.filter((_, i) => i !== index);
        preview_images = preview_images.filter((_, i) => i !== index);
        reference = !!feature_images.length;
    }
</script>

<div
    on:click={() => visible = false}
    class={[
        'fixed top-0 left-0 w-full h-full bg-black/60 backdrop-blur z-10 transition',
        visible ? '' : 'opacity-0 pointer-events-none'
    ].join(' ')}
></div>

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

    <Label for="feature_images" class="uppercase text-sm opacity-60 font-bold">Upload Figma designs:</Label>
    <div class="mt-2 text-center">
        <Dropzone
            on:drop={handleFilesSelect}
            accept="image/*"
            containerClasses="!rounded-lg"
        />
    </div>

    {#if preview_images.length}
       <div class="grid grid-cols-2 gap-2 mt-4">
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
    {/if}
</aside>