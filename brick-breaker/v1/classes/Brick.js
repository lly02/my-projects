import { Block } from "./block.js";

export class Brick extends Block{
    constructor(block, col, row){
        super(block.getHeight(), block.getLength(), block.getMaxCol(), block.getMaxRow());

        this.col = col;
        this.row = row;
    };

    getCol(){
        return this.col;
    };

    getRow(){
        return this.row;
    };

    setCol(col){
        this.col = col;
    };

    setRow(row){
        this.row = row;
    };
};