# TeaQL - A Safe, Simple, Unified Generative based versatile query library for various data sources .


## Feature

* One query do all with connected data
* Graph theory based query
* Fine grained columns and filters
* Different data in a single query

## This is how ChatGPT explain our query


## Examples

Select All families

```java

Q.families()

```
Select All families and their kids

```java

Q.families().selectKidList()

```

Select families has kids

```java

Q.families().hasKids()

```

Select families has kids boy

```java

Q.families().hasKids(Q.kids().whosGenderIsBoy())

```

Select families and count kid girls.

```java

Q.families().countKids("kidGirlsCount",Q.kids().whosGenderIsGirl())

```

Summarize the age of all kids of the families

```java
    public Object hello(WechatMessagingUserContext userContext) throws Exception {
        return  Q.families()
		.selectKidList()
		.averageAgeOfKids(Q.kids())
		.summarizeAgeOfKids(Q.kids())
		.countKids(Q.kids())
		.executeForList(userContext);
    }


```


