module.exports = function(eleventyConfig) {
  // ブログ用のCSSをそのまま出力先にコピー
  eleventyConfig.addPassthroughCopy("blog/css");
  eleventyConfig.addPassthroughCopy("blog/images");

  // 記事のコレクションを作成（日付順）
  eleventyConfig.addCollection("posts", function(collectionApi) {
    return collectionApi.getFilteredByGlob("blog/posts/*.md").sort(function(a, b) {
      return b.date - a.date;
    });
  });

  // 日付フォーマット用フィルター
  eleventyConfig.addFilter("dateFormat", function(date) {
    var d = new Date(date);
    return d.getFullYear() + '/' + 
      String(d.getMonth() + 1).padStart(2, '0') + '/' + 
      String(d.getDate()).padStart(2, '0');
  });

  return {
    dir: {
      input: "blog",
      output: "_site/blog",
      includes: "_includes",
      data: "_data"
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk"
  };
};
