const util = require('util');
const fs = require('fs/promises');
const download = require('download-git-repo');
const { ChainsRepository } = require('./repositories');

const downloadRepo = util.promisify(download);

const CHAINS_REPO = 'ethereum-lists/chains';
const CHAINS_LOCAL_PATH = `sources/${CHAINS_REPO}`;

/**
 * Entry point. Downloads the target repo, gets all the chains data,
 * and writes the result to a result.txt file.
 */
(async () => {
  await downloadRepo(CHAINS_REPO, CHAINS_LOCAL_PATH);
  const chains = await ChainsRepository.getAllChains(CHAINS_LOCAL_PATH);

  const result = chains.map((ch) => `${ch?.name} = ${ch?.id}\n`);
  await fs.writeFile('result.txt', result);
})();
