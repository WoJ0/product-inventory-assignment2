# Pushing this project to GitHub

1. Create a new **empty** repository on GitHub (e.g. `product-inventory-assignment2`).
   Do **not** add a README/license (this project already has one).

2. In a terminal, inside the `product-inventory` folder:

```bash
git init
git add .
git commit -m "Assignment 2: Flask product inventory with REST web-services"
git branch -M main
git remote add origin https://github.com/<your-username>/product-inventory-assignment2.git
git push -u origin main
```

3. Copy the repository URL (e.g. `https://github.com/<your-username>/product-inventory-assignment2`)
   — that is the **GitHub link** you submit.

> The `.gitignore` already excludes the database, virtual environment, and cache
> files so only source code is uploaded.
