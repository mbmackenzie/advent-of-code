use std::fs;

fn main() {
    let file_path = ".aoc_cache/2022_01.txt";
    let contents = fs::read_to_string(file_path).unwrap();

    let mut elves: Vec<i32> = Vec::new();
    let mut elf = 0;

    for line in contents.lines() {
        if line.trim().len() == 0 {
            elves.push(elf);
            elf = 0;
            continue;
        }

        let number = line.trim().parse::<i32>().unwrap();
        elf += number;
    }

    println!("Part 1: {}", elves.iter().max().unwrap());

    elves.sort();
    let sum = elves.into_iter().rev().take(3).sum::<i32>();

    println!("Part 2: {}", sum);
}
