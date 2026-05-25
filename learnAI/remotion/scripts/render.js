const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const publicVideosDir = path.join(__dirname, '../public/videos');

// Mapping of video filenames to their USB locations
const videoSources = {
  'DJI_20260124104255_0004_D.MP4': '/Volumes/USB/drone/walk/DJI_20260124104255_0004_D.MP4',
  'DJI_20260124110814_0005_D.MP4': '/Volumes/USB/drone/run/DJI_20260124110814_0005_D.MP4',
  'DJI_20260124112727_0006_D.MP4': '/Volumes/USB/drone/run/DJI_20260124112727_0006_D.MP4',
  'DJI_20260124112826_0007_D.MP4': '/Volumes/USB/drone/run/DJI_20260124112826_0007_D.MP4',
  'DJI_20260124113216_0008_D.MP4': '/Volumes/USB/drone/walk/DJI_20260124113216_0008_D.MP4',
  'DJI_20260124131820_0009_D.MP4': '/Volumes/USB/drone/walk/DJI_20260124131820_0009_D.MP4',
};

// Function to replace symlinks with actual file copies
function copyRealFiles() {
  console.log('Replacing symlinks with actual file copies to facilitate rendering...');
  for (const [filename, usbPath] of Object.entries(videoSources)) {
    const destPath = path.join(publicVideosDir, filename);
    
    // Check if the destination exists and is a symlink
    try {
      const stats = fs.lstatSync(destPath);
      if (stats.isSymbolicLink()) {
        fs.unlinkSync(destPath);
      } else {
        // If it's already a real file, skip copying
        console.log(`- ${filename} is already a real file, skipping.`);
        continue;
      }
    } catch (err) {
      if (err.code !== 'ENOENT') throw err;
    }

    console.log(`- Copying ${filename} from USB...`);
    fs.copyFileSync(usbPath, destPath);
  }
}

// Function to restore symlinks
function restoreSymlinks() {
  console.log('Restoring symlinks to save local disk space...');
  for (const [filename, usbPath] of Object.entries(videoSources)) {
    const destPath = path.join(publicVideosDir, filename);
    try {
      const stats = fs.lstatSync(destPath);
      if (!stats.isSymbolicLink()) {
        fs.unlinkSync(destPath);
        fs.symlinkSync(usbPath, destPath);
        console.log(`- Restored symlink for ${filename}`);
      }
    } catch (err) {
      console.error(`- Failed to restore symlink for ${filename}:`, err.message);
    }
  }
}

try {
  copyRealFiles();
  
  // Forward all CLI arguments to the remotion CLI
  const args = process.argv.slice(2).join(' ');
  const renderCmd = `npx remotion render ${args}`;
  console.log(`Running: ${renderCmd}`);
  
  execSync(renderCmd, { stdio: 'inherit' });
} catch (err) {
  console.error('Render failed:', err.message);
  process.exitCode = 1;
} finally {
  restoreSymlinks();
}
