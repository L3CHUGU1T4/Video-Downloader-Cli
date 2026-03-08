class Ytdl < Formula
  include Language::Python::Virtualenv

  desc "Descargador interactivo de YouTube: MP4 con video + audio"
  homepage "https://github.com/tu-usuario/ytdl"
  url "https://github.com/tu-usuario/ytdl/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "REEMPLAZA_CON_SHA256_REAL"  # sha256sum v1.0.0.tar.gz
  license "MIT"

  depends_on "python@3.12"
  depends_on "ffmpeg"

  # Genera los bloques resource con:
  #   poet ytdl  (pip install homebrew-pypi-poet)
  resource "certifi" do
    url "https://files.pythonhosted.org/packages/..."
    sha256 "..."
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/..."
    sha256 "..."
  end

  resource "yt-dlp" do
    url "https://files.pythonhosted.org/packages/..."
    sha256 "..."
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "usage", shell_output("#{bin}/ytdl --help 2>&1", 1)
  end
end
