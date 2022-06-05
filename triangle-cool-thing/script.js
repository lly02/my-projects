const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');
const dpr = window.devicePixelRatio;
const rect = canvas.getBoundingClientRect();

// Canvas dimensions
let width = 800;
let height = 800;

canvas.width = width * dpr;
canvas.height = height * dpr;

ctx.scale(dpr, dpr)

canvas.style.width = width + 'px';
canvas.style.height = height + 'px';

// Border to make triangle clean
drawing_border = 5;

// Set the midpoint for top of triangle
midpoint_x = Math.floor(canvas.width/2);

// Draw the first three points
point_a = [midpoint_x, drawing_border];
point_b = [drawing_border, canvas.height-drawing_border];
point_c = [canvas.width-drawing_border, canvas.height-drawing_border];

draw(point_a);
draw(point_b);
draw(point_c);

// Generate first_point until inside triangle
let vertex_active;

while(true){
    flag = false;

    vertex_active = first_random_point();

    flag = random_point_check(point_a, point_b, point_c, vertex_active);
    console.log(flag)
    if(flag) {
        draw(vertex_active);
        break;
    };
}

let loop = 1000;
// Loop the actual pattern
for(i=0; i<loop; i++){
    let random_vertex = Math.ceil(Math.random() * 3);
    let vertex_compare;
    
    if(random_vertex == 1) vertex_compare = point_a;
    if(random_vertex == 2) vertex_compare = point_b;
    if(random_vertex == 3) vertex_compare = point_c;

    vertex_active = get_midpoint(vertex_active, vertex_compare);

    draw(vertex_active);
}

// Provide 2 points; Draw.
function draw(a) {
    ctx.fillRect(a[0], a[1], 1, 1)
}

// Check if random point is inside triangle
function random_point_check(a,b,c,m){
    // Logic (0 < AM.AB < AB.AB) ^ (0 < AM.AC < AC.AC)

    // Distance of vectors
    am = [m[1] - a[1], m[0] - a[0]];
    ab = [b[1] - a[1], b[0] - a[0]];
    ac = [c[1] - a[1], c[0] - a[0]];

    am_ab = [am[0]*ab[0] + am[1]*ab[1]];
    ab_ab = [ab[0]*ab[0] + ab[1]*ab[1]];
    am_ac = [am[0]*ac[0] + am[1]*ac[1]];
    ac_ac = [ac[0]*ac[0] + ac[1]*ac[1]];

    return ((0 < am_ab < ab_ab) && (0 < am_ac < ac_ac));
}

// Get first random point
function first_random_point(){
    rand_x = drawing_border + Math.ceil(Math.random() * (canvas.width - drawing_border * 2));
    rand_y = drawing_border + Math.ceil(Math.random() * (canvas.height - drawing_border * 2));

    return [rand_x, rand_y];
}

// Get midpoint of 2 vertices
function get_midpoint(a, b){
    // X midpoint
    let x = Math.ceil((a[0]+b[0])/2);

    // Y midpoint
    let y = Math.ceil((a[1]+b[1])/2);

    return [x, y];
}