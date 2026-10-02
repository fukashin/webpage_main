module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/image");
  eleventyConfig.addPassthroughCopy("src/img");
  eleventyConfig.addPassthroughCopy("src/blog/css");

  // ブログ記事（新しい順）
  eleventyConfig.addCollection("posts", function (collectionApi) {
    return collectionApi.getFilteredByGlob("src/blog/posts/*.md").sort(function (a, b) {
      return b.date - a.date;
    });
  });

  eleventyConfig.addFilter("dateFormat", function (date) {
    var d = new Date(date);
    return d.getFullYear() + "/" +
      String(d.getMonth() + 1).padStart(2, "0") + "/" +
      String(d.getDate()).padStart(2, "0");
  });

  // OGP や sitemap 用。url フィルタを通した後のパスに site.url（オリジン）を付ける
  eleventyConfig.addFilter("absolute", function (path, origin) {
    return String(origin).replace(/\/$/, "") + path;
  });

  eleventyConfig.addFilter("youtubeThumb", function (id) {
    return "https://img.youtube.com/vi/" + id + "/hqdefault.jpg";
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data"
    },
    // GitHub Pages のプロジェクトサイト（/webpage_main/）で配信するときは
    // PATH_PREFIX=/webpage_main/ を付けてビルドする。独自ドメインでは不要
    pathPrefix: process.env.PATH_PREFIX || "/",
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk"
  };
};
