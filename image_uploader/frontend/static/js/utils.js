
function updateImages() {
    $.get('webservice/get-images').then(
        function(response) {
            // Build data and fill list
            let images = [];
            for (let image of response.images) {
                images.push(buildImageElement(image));
            }

            $("#image-list").empty();
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

    let elementImage = $("<img />").attr("src", image.image)
                        .css('max-width', '180px')
                        .css('max-height', '180px');
    return $("<div></div>").append(elementImage)
        .addClass("image-container")
        .append(crops)
        .click(getCropperBuilder(image));
}

function buildCropElement(crop) {
    let cropImage = $("<img />")
        .attr("src", crop.image)
        .css('max-width', '180px')
        .css('max-height', '180px');
    return $("<div></div>")
        .addClass("image-container")
        .append($("<span></span>").text(crop.metadata))
        .append(cropImage);
}

function getCropperBuilder(image) {
    return function() {
        window.cropperController.clean();
        window.cropperController.setImage(image);

        // Mark default woman
        $("#female-gender").attr("checked", true);
        window.cropperController.setGender('f');
    };
}