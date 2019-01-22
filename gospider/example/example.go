package main

import (
	"bytes"
	"github.com/PuerkitoBio/goquery"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
)

func check(err error, msg string) {
	if err != nil {
		log.Fatalln(msg, err.Error())
	}
}

func main() {
	go func() {
		for {
			println(1)
		}
	}()
	println("over")
}

func amain() {
	root := "http://www.zeroorez.net/beauty"
	client := &http.Client{}

	req, err := http.NewRequest("GET", root, nil)
	check(err, "Failed to create request!")

	resp, err := client.Do(req)
	check(err, "Failed to request the url!")

	reader := resp.Body.(io.Reader)
	body, err := ioutil.ReadAll(reader)
	check(err, "Failed to read data from response!")

	pageUrl, err := url.Parse(root)
	check(err, "Failed to parse root url!")
	log.Println("Page url is", pageUrl.String())

	doc, err := goquery.NewDocumentFromReader(bytes.NewReader(body))
	check(err, "Failed to create document!")
	log.Println("Successfully generate query document")

	doc.Find(".post > .text > .post-content > a").Each(func(i int, selection *goquery.Selection) {
		href, exist := selection.Attr("href")
		if !exist || href == "" {
			return
		}
		if selection.Text() == "[查看原图]" {
			println("图片链接", i, href)
		}
	})

	/*
		doc.Find("img").Each(func(i int, selection *goquery.Selection) {
			imgUrl, exists := selection.Attr("src")
			if !exists || imgUrl == "" {
				return
			}
			log.Println("The", i, "image's url is", imgUrl)

			var buffer bytes.Buffer
			if lower := strings.ToLower(imgUrl); strings.Index(lower, "http://") == 0 || strings.Index(lower, "https://") == 0 {
				buffer.WriteString(lower)
			} else {
				buffer.WriteString(pageUrl.Scheme)
				buffer.WriteString("://")
				buffer.WriteString(pageUrl.Host)

				switch lower[0] {
				case '?':
					if len(pageUrl.Path) == 0 {
						buffer.WriteByte('/')
					} else {
						buffer.WriteString(pageUrl.Path)
					}
					buffer.WriteString(lower)
				case '/':
					buffer.WriteString(lower)
				default:
					pt := "/" + path.Dir(pageUrl.Path) + "/" + lower
					buffer.WriteString(path.Clean(pt))
				}
			}
			absPath, err := url.Parse(buffer.String())
			if err != nil {
				log.Fatalln("Failed to convert img path to absolute path!", err.Error())
			}

			// 删除锚点
			absPath.Fragment = ""
			absUrl := absPath.String()
			// 文件名规则
			filename := "tmp/" + path.Base(pageUrl.String()) + "_" + strconv.Itoa(i) + path.Ext(imgUrl)
			log.Println("The", i, "image's absolute url is", absUrl)
			log.Println("Filename to save the image:", filename)

			// 下载图片
			req, err := http.NewRequest("GET", absUrl, nil)
			if err != nil {
				log.Fatalln("Failed to create request!", err.Error())
			}

			resp, err := client.Do(req)
			if err != nil {
				log.Fatalln("Failed to request the url!", err.Error())
			}

			img, err := os.Create(filename)
			if err != nil {
				log.Fatalln("Failed to create file!", err.Error())
			}

			imgWriter := bufio.NewWriterSize(img, 1024)
			_, err = io.Copy(imgWriter, resp.Body)
			if err != nil {
				log.Fatalln("Failed to copy from response body!", err.Error())
			}

			err = imgWriter.Flush()
			check(err, "Failed to flush!")

			log.Println("Successfully fetch a image!")
		})
	*/
}
