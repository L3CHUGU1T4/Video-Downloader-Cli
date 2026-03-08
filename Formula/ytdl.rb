class Ytdl < Formula
  include Language::Python::Virtualenv

  desc "Descargador interactivo de YouTube: MP4 con video + audio"
  homepage "https://github.com/L3CHUGU1T4/Video-Downloader-Cli"
  url "https://github.com/L3CHUGU1T4/Video-Downloader-Cli/archive/refs/tags/v1.0.1.tar.gz"
  sha256 "ebeb89bab57d44ae928c1590e55520b0fb481628eee38620aa9cc0a62c66ada7"
  license "MIT"

  depends_on "python@3.12"
  depends_on "ffmpeg"

  resource "l3chu-ytdl" do
    url "https://files.pythonhosted.org/packages/py3/l/l3chu_ytdl/l3chu_ytdl-1.0.0-py3-none-any.whl"
    sha256 "136e53c857ed94cd9c1f3482487342f72fe43c5fe5c520bb06d7d182fe4d7ce2"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/py3/r/rich/rich-14.3.3-py3-none-any.whl"
    sha256 "793431c1f8619afa7d3b52b2cdec859562b950ea0d4b6b505397612db8d5362d"
  end

  resource "yt-dlp" do
    url "https://files.pythonhosted.org/packages/py3/y/yt_dlp/yt_dlp-2026.3.3-py3-none-any.whl"
    sha256 "166c6e68c49ba526474bd400e0129f58aa522c2896204aa73be669c3d2f15e63"
  end

  def install
    virtualenv_install_with_resources
    bin.install libexec/"bin/ytdl"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/ytdl --version 2>&1", 1)
  end
end