function getCookie(name) {
  const cookies = decodeURIComponent(document.cookie).split(';');

  for (const cookie of cookies) {
    const trimmed = cookie.trim();
    if (trimmed.startsWith(name + '=')) {
      return trimmed.slice(name.length + 1);
    }
  }
  return '';
}