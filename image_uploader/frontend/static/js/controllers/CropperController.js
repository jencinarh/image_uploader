/**
 * Useful class to keep the state of the current crop
 */
class CropperController {
    constructor(imageService) {
        this.imageService = imageService;
        this.image = null;
        this.coords = {};
        this.gender = null;

        this.view = $('#cropper-preview');
    }

    /**
     * Select the current image to crop it
     * @param image
     */
    setImage(image) {
        this.image = image;
        this.view.attr('src', image.image);
        let self = this;
        this.view.Jcrop({
            onSelect: function (coords) {
                self.coords = coords;
                console.log(self.coords);
            }
        });
    }

    setGender(gender) {
        this.gender = gender;
    }

    clean() {
        this.view.empty();
        this.image = null;
        this.coords = {};
    }

    getCrop() {
        console.log(this.coords);
        return {
            'x': this.coords['x'],
            'y': this.coords['y'],
            'x2': this.coords['x2'],
            'y2': this.coords['y2'],
        }
    }

    cropImage() {
        if (this.image == null) {
            return;
        }

        console.log(this);
        let crop = this.getCrop();
        this.imageService.cropImage(this.image.id, crop, this.gender).then(
            x => console.log("Successful")
        );
    }
}