let win_count = 0;
let lose_count = 0;

// Loop number of times to test
for(let i = 0; i < 1000; i++){
    // Select prize doorl
    let prize_door = select_random_door();
    let chosen_door = select_random_door();
    console.log(chosen_door)
    let reveal_door;

    while(true){
        // Choose door to reveal, check whether it is same as chosen_door and prize_door
        reveal_door = select_random_door();

        if(reveal_door !== chosen_door && reveal_door !== prize_door){
            // Switch chosen door
            while(true){
                let switch_door = select_random_door();
                console.log(switch_door)
                if(switch_door !== reveal_door && switch_door !== chosen_door) {
                    chosen_door = switch_door;
                    break;
                }
            };

            break;
        };
    };

    if(chosen_door == prize_door) {
        win_count++;
        document.getElementById("win-count").innerText = win_count;
    }
    else {
        lose_count++;
        document.getElementById("lose-count").innerText = lose_count;
    }

    let win_percent = Math.ceil((win_count/(lose_count + win_count)) * 100);
    document.getElementById("win-percent").innerText = win_percent + "%";

    console.log(`Prize door: ${prize_door}, Chosen door: ${chosen_door}, Reveal door: ${reveal_door}, Win: ${win_count}, Lose: ${lose_count}`)
};

function select_random_door(){
    return Math.ceil(Math.random()*3);
};