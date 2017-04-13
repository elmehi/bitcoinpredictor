db.scraped1m.aggregate([{
    $group: {
        _id: "$date",
        text: {
            $addToSet: "$text"
        },
        retweets: {
            $addToSet: "$retweets"
        },
        favorites: {
            $addToSet: "$favorites"
        },
        count: {
            $sum: 1
        },
        retweets_total: {
            $sum: "$retweets"
        },
        favorites_total: {
            $sum: "$favorites"
        }
    },
}, {
    $out: "scraped1agg"
}])

db.twitter_two_copy.aggregate(
   [ { 
    $sample: { size: 5 }},
    {$out: "twitter_two_sample"}
  ])

db.twitter_two_sample.find().snapshot().forEach(
    function(e) {
        e.date.setSeconds(0)
        // save the updated document
        db.twitter_two_sample.save(e);
    }
)



db.scraped1.find().snapshot().forEach(
    function(e) {
        e.seconds = e.date.getSeconds();
        e.date.setSeconds(0);
        db.scraped1m.save(e);
    }
)