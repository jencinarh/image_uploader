
function updateImages() {
    $.get('webservice/get-images').then(
        function(response) {
            // Build data and fill list
            let images = [];
            for (let image of response.images) {
                images.push(buildImageElement(image));
            }

            // Update the list
            $("#image-list").append(images);
        }
    )
}

function buildImageElement(image) {
    let crops = [];
    for (let crop of image.crops) {
        crops.push(
            buildCropElement(crop)
        );
    }

    return $("div").append(crops);
}

function buildCropElement(crop) {

    return $("div").append(
        $("span").text(crop.metadata)
    ).append(
        $("img").attr("src", crop.image)
    );
}