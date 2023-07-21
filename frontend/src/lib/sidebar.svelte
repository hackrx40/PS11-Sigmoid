<script>
    import { Label, Toggle } from "flowbite-svelte";
    import Dropzone from "svelte-file-dropzone/Dropzone.svelte";
    import { XIcon } from "svelte-feather-icons";

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

<aside class="bg-white p-4 w-[400px] border-l border-primary overflow-y-auto">
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

    <Label for="filters" class="uppercase text-sm opacity-60 font-bold mt-6">Filters:</Label>
    <div class="mt-2 flex flex-col gap-2">
        <Toggle
            checked={reference}
            disabled={!feature_images.length}
            class={!feature_images.length && 'opacity-50'}
            on:change={() => reference = !reference}
        >Enable Reference Comparison</Toggle>
        <Toggle
            checked={filters.button}
            disabled={!reference}
            class={!reference && 'opacity-50'}
        >Compare 'Button'</Toggle>
        <Toggle
            checked={filters.text}
            disabled={!reference}
            class={!reference && 'opacity-50'}
        >Compare 'Text'</Toggle>
        <Toggle
            checked={filters.image}
            disabled={!reference}
            class={!reference && 'opacity-50'}
        >Compare 'Image'</Toggle>
        <Toggle
            checked={filters.link}
            disabled={!reference}
            class={!reference && 'opacity-50'}
        >Compare 'Link'</Toggle>
    </div>
</aside>