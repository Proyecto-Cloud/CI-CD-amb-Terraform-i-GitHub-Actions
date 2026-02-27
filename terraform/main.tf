# ---------- DATA ----------
# Gets the list of available azs in the defined region.
data "aws_availability_zones" "available_zones" {
  state = "available"
}
