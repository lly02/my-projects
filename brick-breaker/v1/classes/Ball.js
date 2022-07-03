export class Ball{
    constructor(radius, pos, speed){
        this.radius = radius;
        this.pos = pos;
        this.speed = speed;
        this.direction = this.randomDirection();
    };

    getRadius(){
        return this.radius;
    };

    getPos(){
        return this.pos;
    };

    getSpeed(){
        return this.speed;
    };

    getDirection(){
        return this.direction;
    };

    setRadius(radius){
        this.radius = radius;
    };

    setPos(pos){
        this.pos = pos;
    };

    setSpeed(speed){
        this.speed = speed;
    };
    
    setDirection(direction){
        this.direction = direction;
    };

    randomDirection(){
        return Math.random() * (2 * Math.PI);
    };

    setNextPos(deltaTime){
        // X, Y
        let newPos = [];

        newPos[0] = this.pos[0] + Math.cos(this.direction) * this.speed * deltaTime/1000;
        newPos[1] = this.pos[1] + Math.sin(this.direction) * this.speed * deltaTime/1000;
        
        this.pos = newPos;
    };
};