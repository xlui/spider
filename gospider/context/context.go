package context

import "sync"

type Context struct {
	PageLock     sync.RWMutex
	PageState    map[string]int
	ImageLock    sync.RWMutex
	ImageState   map[string]int
	PageChannel  chan *Page
	ParseChannel chan *Page
	ImageChannel chan *Image
	ImageCount   chan int
}
