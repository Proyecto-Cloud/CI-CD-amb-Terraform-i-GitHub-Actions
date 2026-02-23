# ---------- DATA ----------
# Gets the list of available azs in the defined region.
data "aws_availability_zones" "available" {
  state = "available"
}

#git branch
#git add .
#git commit -m "Mensaje claro del cambio"
#git push origin feature/ci-workflow
#Ve al repo en GitHub.
#Aparecerá botón amarillo:
#Compare & pull request
#Haz clic.
#Asegúrate:
#Base: main
#Compare: feature/ci-workflow
#Pulsa Create pull request.