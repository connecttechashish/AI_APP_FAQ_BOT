# Rebuild the FAISS index from the FAQ content
$repoRoot = Join-Path $PSScriptRoot '..'
$venvPath = Join-Path $repoRoot '.venv'

Push-Location $repoRoot
try {
  $cmd = "from model.indexer import load_faq_chunks; from model.embedding import load_embedding_model; from model.vectorstore import build_index; chunks=load_faq_chunks('data/faq.md'); model=load_embedding_model(); build_index(chunks, model)"
  & (Join-Path $venvPath 'Scripts\python.exe') -c $cmd
} finally {
  Pop-Location
}
