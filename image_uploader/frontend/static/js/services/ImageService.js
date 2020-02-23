

class ImageService {

    cropImage(id, coords, gender) {
        let defer = $.Deferred();

        let data = {
            id: id,
            coords: coords,
            metadata: {gender: gender},
        };

        console.log(data);
        $.ajax({
            type: "POST",
            url:"/webservice/crop-image",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify(data),
        }).then(function(response) {
            defer.resolve(response)
        });

        return defer.promise();
    }

    getImages() {

    }

    uploadImage() {

    }
}