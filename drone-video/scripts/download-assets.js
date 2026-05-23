const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const assets = [
  {
    url: 'https://upload.wikimedia.org/wikipedia/commons/8/82/Nocturne_in_E_flat_major%2C_Op._9_no._2.mp3',
    dest: 'music.mp3'
  },
  {
    url: 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Howling_wind.ogg',
    dest: 'wind.ogg'
  },
  {
    url: 'https://upload.wikimedia.org/wikipedia/commons/3/38/Birds_forest.ogg',
    dest: 'birds.ogg'
  }
];

const publicDir = path.join(__dirname, '../public');

if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

function downloadFile(url, destPath) {
  console.log(`Downloading ${url} to ${destPath}...`);
  const userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
  const command = `curl -L -A "${userAgent}" -o "${destPath}" "${url}"`;
  execSync(command, { stdio: 'inherit' });
  console.log(`Finished downloading ${destPath}`);
}

function main() {
  for (const asset of assets) {
    const destPath = path.join(publicDir, asset.dest);
    try {
      downloadFile(asset.url, destPath);
    } catch (err) {
      console.error(`Error downloading ${asset.dest}:`, err.message);
    }
  }
  console.log('All downloads completed!');
}

main();
