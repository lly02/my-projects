export class Platform{
    constructor(length, height, pos, speed){
        this.platform_length = length;
        this.platform_height = height;
        this.platform_pos = pos;
        this.platform_speed = speed;
    };

    getLength(){
        return this.platform_length;
    };

    getHeight(){
        return this.platform_height;
    };

    getPos(){
        return this.platform_pos;
    };

    getSpeed(){
        return this.platform_speed;
    };

    setLength(length){
        this.platform_length = length;
    };

    setHeight(height){
        this.platform_height = height;
    };

    setPos(pos){
        this.platform_pos = pos;
    };

    setSpeed(speed){
        this.platform_speed = speed;
    };
}