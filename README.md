# USTC-Web-Info

## Download

```shell
$ git clone git@github.com:IcePear-Jzx/USTC-Web-Info.git
```

## Lab-0-Web-Spider

### Problem

[Douban](https://www.douban.com) is a community website where users give comments about books, movies, music and so on. 
The goal of this lab is to use web spider to get books' information from [Douban Books](https://book.douban.com).

* Get the top 250 book's information
* Get all books' URLs
* Design distributed technique or parallel technique

More details:
[https://git.bdaa.pro/yxonic/data-specification/wikis/豆瓣%20书评](https://git.bdaa.pro/yxonic/data-specification/wikis/豆瓣%20书评)

### Installation

```shell
$ pip3 install lxml --user
```

### Usage

Take about 40 minutes totally depending on the quality of proxies.
(Suggest testing at midnight.)

#### 1. Buy proxies

Buy proxies from [虎头代理](http://ip.hutoudaili.com). 
Copy all proxies to proxies.txt.

**Notice: The proxies are really unstable, I need to update proxies frequently. Please contact me before testing so I can update these proxies.**

#### 2. Filter proxies

Filter available proxies and save them in proxies.json.

```shell
$ python3 proxy_filter.py
```

#### 3. Crawl

```shell
$ python3 spider.py
```

This will take a very long time depending on the quality of proxies.

If you see something like:

```shell
HTTPError: https://book.douban.com/subject/1089243/
Delete: {"https": "128.23.214.22:8080"}
```

Don't worry about them, the spider will automatically deal with them. 

If you see:

```shell
Get 你好，旧时光（上 下) Error! URL: https://book.douban.com/subject/4166819/
```

This is because [https://book.douban.com/subject/4166819/](https://book.douban.com/subject/4166819/) doesn't exist.

#### 4. Results

Open JSON file to see what you have got.

### Explanation

#### 1. Top 250 books

Firstly, get the top 250 books' URLs from [https://book.douban.com/top250](https://book.douban.com/top250).

You can see there are 25 books in one page, and every page has its own URL such as [https://book.douban.com/top250?start=0](https://book.douban.com/top250?start=0) and [https://book.douban.com/top250?start=25](https://book.douban.com/top250?start=25).

Only need to change the number after "start=".

Then, visit every book's URL to get more information. For example, [https://book.douban.com/subject/1770782/](https://book.douban.com/subject/1770782/).

Notice: some books' URLs don't exist such as [你好，旧时光（上 下)](https://book.douban.com/subject/4166819/).

As for longRemark("书评"), you need to click "展开" to get full content such as [https://book.douban.com/subject/1770782/reviews](https://book.douban.com/subject/1770782/reviews). 

To deal with that, I analyzed the javascript file, and found out that they use ajax to apply for the full content. For example, [https://book.douban.com/j/review/1476522/full](https://book.douban.com/j/review/1476522/full) which is a json format. The URL format is like [https://book.douban.com/j/review/<review_id>/full]().

#### 2. All books' URLs

At first, get all tags from [https://book.douban.com/tag/?view=cloud](https://book.douban.com/tag/?view=cloud). 

Then, get all books' URLs in each tag. However, there are only 50 pages shown in a single tag. 
See [https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6?start=980](https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6?start=980)
and [https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6?start=1000](https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6?start=1000).
The latter doesn't show any books' information. Thus we can only get 1000 books' URLs in one tag.

To get more books' URLs, we can notice that in any book's page, there are some similar books recommended to readers. Get their URLs and add to book list.

#### 3. Parallel technique

In function `get_top250_detail()` and `get_all_url()`, I use parallel technique. A `multiprocessing.Pool` contains 20 processes, and `multiprocessing.Manager()` is used to share data among processes.
