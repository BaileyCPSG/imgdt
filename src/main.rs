use std::process;
use clap::Parser;

use imgdt::Config;

fn main() {
    let config: Config = Parser::parse();
    println!("{:?}", config);
    if let Err(err) = imgdt::run(config).await {
        eprintln!("Error running example: {}", err);
        process::exit(1);
    }
}
