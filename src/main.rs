use std::error::Error;
use std::process;

use serde::Deserialize;
use clap::Parser;

fn main() {
    let config: Config = Parser::parse();
    println!("{:?}", config);
    // if let Err(err) = example() {
    //     eprintln!("Error running example: {}", err);
    //     process::exit(1);
    // }
}

/// Download images from a csv file with Rust!
#[derive(Debug, Parser)]
#[clap(author, version)]
struct Config {
    /// path to the input file
    input_file: String,
    /// directory to store the downloaded files
    #[clap(short='o', default_value=".")]
    download_dir: String,
}

// #[derive(Debug, Deserialize)]
// struct Record {
//     url: String,
//     filename: String,
// }
// 
// fn example() -> Result<(), Box<dyn Error>> {
//     let mut rdr = csv::Reader::from_path("test.csv")?;
//     for result in rdr.deserialize() {
//         let record: Record = result?;
//         println!("{:?}", record);
//     }
//     Ok(())
// }
