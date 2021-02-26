<p align="center">
  <a href="https://www.deployboard.io"><img src="https://user-images.githubusercontent.com/7454248/108596582-f253f380-7353-11eb-838d-18f44478a67a.png" alt="DeployBoard"></a>
</p>
<p align="center">
  Measure the success of DevOps in your organization.
</p>
<p align="center">
  <a href="https://github.com/DeployBoard/deployboard/actions?query=workflow%3ATest+branch%3Amain" target="_blank">
    <img src="https://github.com/DeployBoard/deployboard/workflows/Test/badge.svg" alt="Test">
  </a>
  <a href="https://codecov.io/gh/DeployBoard/deployboard" target="_blank">
    <img src="https://codecov.io/gh/DeployBoard/deployboard/branch/main/graph/badge.svg" alt="Coverage">
  </a>
</p>

---

- Simple deployment tracking tool.
- Easily plugs in to any deployment tool or pipeline.
- Tracks DORA metrics, compliance, and more.

## Deployment

Build bootstrap with our custom scss from the root of this repository.

`bash scripts/build_bootstrap.sh`

Start the app.

`docker-compose up -d`

## Development

Virtual Environment

`python3 -m venv venv`

`source venv/bin/activate`

Start the app via docker.

`docker-compose up -d`
