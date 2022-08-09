export class Block{
    constructor(height, length, max_col, max_row){
        this.height = height;
        this.length = length;
        this.max_col = max_col;
        this.max_row = max_row;
    };

    getHeight(){
        return this.height;
    };

    getLength(){
        return this.length;
    };

    getMaxCol(){
        return this.max_col;
    };

    getMaxRow(){
        return this.max_row;
    };

    setHeight(){
        this.height = height;
    };

    setLength(){
        this.length = length;
    };

    setMaxCol(){
        this.max_col = max_col;
    };

    setMaxRow(){
        this.max_row = max_row;
    };
};