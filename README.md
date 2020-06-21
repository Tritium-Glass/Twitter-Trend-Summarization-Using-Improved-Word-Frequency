# Final-Year-Project
<h2>TWITTER BOT FOR SUMMARIZING ARTICLES BASED ON TWITTER TRENDS</h2>

<br>

<div>
  <p>Working of the software:
    <ul>
      <li>the Twitter interface interface takes the top few trending topics from Twitter, cleans them, and sends them to Web Scraping module</li>
      <li>the Web Scraping module searches the web for articles related to that topic that are most recent and are from trusted sources and then forwards them to the text summarization module</li>
      <li>the text summarization module uses a modified word frequency method to get the gist of the news article in fewer than 240 characters and then sends it to the Twitter interface module</li>
      <li>a shortened hyperlink to the article is appended to the short gist, and the final result is posted on Twitter</li>
  </ul>
 </p>
</div>

<br>

<div>
  <p>For selecting the most appropriate extractive summarization method, the following algorithms were compared:
    <ol>
      <li>Word Frequency</li>
      <li>Term Frequency - Inverse Document Frequency</li>
      <li>TextRank</li>
      <li>Latent Semantic Analysis</li>
      <li>Improved Word Frequency (we modified the word frequency algorithm)</li>
  </ol>
  </p>
  </div>
      

  
