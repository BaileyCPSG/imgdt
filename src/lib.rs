use clap::Parser;
use reqwest::Client;
use serde::Deserialize;
use std::error::Error;

/// Download images from a csv file with Rust!
#[derive(Debug, Parser)]
#[clap(author, version)]
pub struct Config {
    /// path to the input file
    pub input_file: String,

    /// directory to store the downloaded files
    #[clap(short='o', default_value=".")]
    pub download_dir: String,
}

#[derive(Debug, Deserialize)]
pub struct Record {
    url: String,
    filename: String,
}

pub async fn run(config: Config) -> Result<(), Box<dyn Error>> {
    let client = Client::new();
    let mut rdr = csv::Reader::from_path(&config.input_file)?;
    for result in rdr.deserialize() {
        let record: Record = result?;
        println!("{:?}", record);
        let response = client.get(record.url).send().await?;
        println!("{}", response.status());
    }


    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn add_test() {
        assert_eq!(4, 2+2);
    }
}
